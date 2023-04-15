FROM public.ecr.aws/lambda/python:3.7

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY main_hubmap.py ${LAMBDA_TASK_ROOT}
COPY main_leukaemia.py ${LAMBDA_TASK_ROOT}
COPY main_chest.py ${LAMBDA_TASK_ROOT}
COPY main_brats.py ${LAMBDA_TASK_ROOT}

COPY hubmap ${LAMBDA_TASK_ROOT}/hubmap
COPY chest ${LAMBDA_TASK_ROOT}/chest
COPY model ${LAMBDA_TASK_ROOT}/model

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "main_hubmap.lambda_handler" ] 