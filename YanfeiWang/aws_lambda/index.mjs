import axios from "axios";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  ScanCommand,
  UpdateCommand
} from "@aws-sdk/lib-dynamodb";

const predict_url = 'https://pzun1eau89.execute-api.us-west-2.amazonaws.com/dev/api-xgboost-model';
const tableName = "iot_simulate"

const client = new DynamoDBClient({});
const dynamo = DynamoDBDocumentClient.from(client);

export const handler = async(event) => {
    const ts1 = event['ts1']; // 1545436697.27
    const ts2 = event['ts2'];
    const predictLabel = event['predictLabel']
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
    if (predictLabel) {
        for (let i =0; i < query.Items.length; i++) {
          const res = await axios.post(predict_url, 
          {"data": query.Items[i].data})
          const label = res.data.body[0] == 'Benign' ? 'Benign' : 'Malicious';
          const detail = label == 'Benign' ? '-' : label;
          const update = await dynamo.send(
            new UpdateCommand({
              TableName: tableName,
              Key: { uid: query.Items[i].uid, ts: query.Items[i].ts},
              UpdateExpression: "set label = :l, detailed_label=:d",
              ExpressionAttributeValues:  {':l' : label, ':d': detail}
            })
          );
          query.Items[i].label = label;
          query.Items[i].detailed_label = detail;
      }
    }
    const response = {
        statusCode: 200,
        body: JSON.stringify(query.Items),
    };
    return response;
};


