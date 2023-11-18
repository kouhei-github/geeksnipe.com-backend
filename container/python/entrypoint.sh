#!/bin/sh
if [ $DEBUG = "True" ]
then
    uvicorn index:app --reload --host 0.0.0.0 --port 8000
else
    uvicorn index:app --reload
fi