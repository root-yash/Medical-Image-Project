import { AttributeType, BillingMode, Table, TableClass } from "aws-cdk-lib/aws-dynamodb";
import { Construct } from "constructs";
import { lambda } from "./lambda";

export class service extends Construct {
    constructor(scope: Construct, id: string){
        super(scope, id);
        const authTable = new Table(this, "Auth-Table",{
            tableName: "Auth-Table",
            partitionKey: {
                name: "AuthID",
                type: AttributeType.STRING,
            },
            billingMode: BillingMode.PAY_PER_REQUEST,
            tableClass: TableClass.STANDARD
        })
        
        new lambda(this, id);

    }
}