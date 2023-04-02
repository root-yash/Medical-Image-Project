import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { service } from './resource/service';

export class AwsResourcesStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // The code that defines your stack goes here
    new service( scope, id);
    // example resource
  }
}
