from fastapi import FastAPI, HTTPException, status
from sklearn.ensemble import RandomForestClassifier
from utils import predict_Target
from schema import RootResponse,ModelRequest,ModelResponse
import logfire
from dotenv import load_dotenv
import os
import uvicorn


# load the environment variables
load_dotenv()
logfire_token = os.getenv(key="LOGFIRE_TOKEN")

# initialize the app
app = FastAPI(title="Endpoint For student dropout Prediction",
              version= "v1")

logfire.configure(token=logfire_token)
logfire.instrument_fastapi(app=app)

# create the root endpoint
@app.get(path="/", tags=["Root Endpoints"], response_model=RootResponse)
def root():
    """This endpoint serves the root api!"""
    return RootResponse(message="We are live!")

# create the prediction endpoint
@app.post(path="/predict/", tags=["target"], response_model=ModelResponse)
def get_Target(payload: ModelRequest):
    """This is the endpoint for the model prediction."""
    try:
        data = payload.model_dump()
        Target = predict_Target(data)
        logfire.info(f"predicted_Target: {Target}, payload: {data}")

        # Extract the value if Target is a dict
        if isinstance(Target, dict):
           if "Target" not in Target:
               logfire.error(f"'Target' key missing in prediction result: {Target}")
               raise HTTPException(
                   status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   detail="'Target' key missing in prediction result"
               )
           Target = Target["Target"]

        elif not isinstance(Target, str):
            logfire.error(f"Unexpected prediction result type: {type(Target)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected prediction result type"
            )
        return ModelResponse(
            predicted_Target=Target
        )

    except Exception as err:
        logfire.error(f"An error occured. Details: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{err}")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8080, reload=True)