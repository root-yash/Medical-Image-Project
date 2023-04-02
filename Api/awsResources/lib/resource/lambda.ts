import { Duration } from "aws-cdk-lib";
import { Effect, ManagedPolicy, PolicyStatement, Role, ServicePrincipal } from "aws-cdk-lib/aws-iam";
import { Code, Function, Runtime } from "aws-cdk-lib/aws-lambda";
import { Construct } from "constructs"
import { ACCOUNT_ID, ML_LAMBDA } from "./constant";

export class lambda extends Construct{
    constructor(scope: Construct, id: string){
        super(scope, id);
        
        // Api Lambda Role
        const apiLambdaRole = new Role( this, `API-Lambda-Role`,{
            roleName: `API-Lambda-Role`,
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
                ManagedPolicy.fromAwsManagedPolicyName('CloudWatchFullAcess')
            ]
        });

        apiLambdaRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                actions: ['dynamo:GetItem', 'lambda:InvokeFunction'],
                resources: [
                    `arn:aws:*:*:${ACCOUNT_ID}:*`
                ]
            })
        )

        // Machine Learning Processing Lambda
        const mlLambdaRole = new Role( this, `ML-Lambda-Role`,{
            roleName: `ML-Lambda-Role`,
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
                ManagedPolicy.fromAwsManagedPolicyName('CloudWatchFullAcess')
            ]
        });

        // Auth Lambda Role
        const authLambdaRole = new Role( this, `AUTH-Lambda-Role`,{
            roleName: `AUTH-Lambda-Role`,
            assumedBy: new ServicePrincipal('lambda.amazonaws.com'),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
                ManagedPolicy.fromAwsManagedPolicyName('CloudWatchFullAcess')
            ]
        });

        authLambdaRole.addToPolicy(
            new PolicyStatement({
                effect: Effect.ALLOW,
                actions: ['dynamo:GetItem'],
                resources: [
                    `arn:aws:*:*:${ACCOUNT_ID}:*`
                ]
            })
        )


        // Lambda function declaration
        const apiLambda = new Function(this, "API-Lambda",{
            functionName: "Api-Lambda",
            description: "check auth and run relevent machine learning model",
            code:  Code.fromAsset("../lambdaLogic/api/lambda_function.py"),
            handler: "lambda_function.lambda_handler",
            memorySize: 256,
            timeout: Duration.seconds(10),
            runtime: Runtime.PYTHON_3_9,
            role: apiLambdaRole
        });

        for ( var mlLambda of ML_LAMBDA ){
            new Function(this, `${mlLambda}-Lambda`,{
                functionName: `${mlLambda}-Lambda`,
                description: "ml model",
                code:  Code.fromAsset(`../lambdaLogic/inferencelogic/${mlLambda}/lambda_function.py`),
                handler: "lambda_function.lambda_handler",
                memorySize: 1024,
                timeout: Duration.seconds(10),
                runtime: Runtime.PYTHON_3_9,
                role: mlLambdaRole
            });
        }

        new Function(this, "Auth-Lambda",{
            functionName: "Auth-Lambda",
            description: "check auth",
            code:  Code.fromAsset("../lambdaLogic/auth/lambda_function.py"),
            handler: "lambda_function.lambda_handler",
            memorySize: 512,
            timeout: Duration.seconds(10),
            runtime: Runtime.PYTHON_3_9,
            role: authLambdaRole
        });
        


    }
}