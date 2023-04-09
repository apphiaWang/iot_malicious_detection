// return predicted simulation IoT requests to front-end
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  ScanCommand,
} from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const dynamo = DynamoDBDocumentClient.from(client);
const tableName = "iot_simulate_data_new";

export const handler = async(event) => {
    const ts1 = event['ts1']; // 1545436697.27
    const ts2 = event['ts2'];
    const query = await dynamo.send(
      new ScanCommand({ 
        TableName: tableName,
        FilterExpression: "ts BETWEEN :ts1 AND :ts2",
        ExpressionAttributeValues: {
            ":ts1": ts1,
            ":ts2": ts2,
        }
      })
    );
    const response = {
        statusCode: 200,
        body: JSON.stringify(query.Items),
    };
    return response;
};
