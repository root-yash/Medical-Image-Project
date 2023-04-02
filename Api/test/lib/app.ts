import { App, DefaultStackSynthesizer } from 'aws-cdk-lib';

// Set up your CDK App
const app = new App();

const applicationAccount = '449773506982';
const bindleGuid = 'amzn1.bindle.resource.5hhybsuqqejdvvdahniq';
const applicationName = 'LeverPostActivationAnalysisTool';


addStage('beta', applicationAccount, 'us-west-2', false);

// Add a stage to pipeline.
function addStage(stageName: string, account: string, region: string, isProd: boolean) {

  const deploymentGroup = stage.addDeploymentGroup({
    name: `${applicationName}-${stageName}`,
  });
  DefaultStackSynthesizer

  const deploymentProps = {
    env: personalBoot
    pipeline.deploymentEnvironmentFor(account, region),
    softwareType: SoftwareType.INFRASTRUCTURE,
    stage: stageName,
  };

  const leverPostActivationAnalysisToolStack = new LeverPostActivationAnalysisToolStack(
    app,
    `${applicationName}-${stageName}`,
    deploymentProps,
  );

  deploymentGroup.addStacks(leverPostActivationAnalysisToolStack);
}