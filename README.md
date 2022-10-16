# AWS Lambda bandwith benchmark

This is a simple benchmark to test the bandwith of AWS Lambda.

## How do AWS Lambda instances scale?

When configuring a Lambda function, you can set the memory size and the timeout. The memory size is the amount of RAM available to the function. 
The timeout is the maximum amount of time the function can run.
The memory size does not only increase the amount of RAM available to the function, but also the CPU power.
To start I created a table with the available memory sizes and the corresponding CPU power. All prices are for the region `eu-central-1` and are in `USD`.

| Memory  | Cores | Speed  | Price per 1ms    |
|---------|-------|--------|------------------|
| 128MB   | 2     | 2,5Ghz | 0,0000000021 USD |
| 512MB   | 2     | 2,5Ghz | 0,0000000083 USD |
| 1024MB  | 2     | 2,5Ghz | 0,0000000167 USD |
| 1536MB  | 2     | 2,5Ghz | 0,0000000250 USD |
| 2048MB  | 2     | 2,5Ghz | 0,0000000333 USD |
| 3072MB  | 3     | 2,5Ghz | 0,0000000500 USD |
| 4096MB  | 3     | 2,5Ghz | 0,0000000667 USD |
| 5120MB  | 3     | 2,5Ghz | 0,0000000833 USD |
| 6144MB  | 4     | 2,5Ghz | 0,0000001000 USD |
| 7168MB  | 5     | 2,5Ghz | 0,0000001167 USD |
| 8192MB  | 5     | 2,5Ghz | 0,0000001333 USD |
| 9216MB  | 6     | 2,5Ghz | 0,0000001500 USD |
| 10240MB | 6     | 2,5Ghz | 0,0000001667 USD |

**Note**: Sometimes the CPU speed was 3.0Ghz instead of 2.5Ghz. But this was not consistent, so I decided to use 2.5Ghz as the CPU speed.

### Deployment

```
$ serverless deploy
```