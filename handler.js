"use strict";
const AWS = require("aws-sdk");
const s3 = new AWS.S3();
const si = require("systeminformation");
const Bucket = "aws-lambda-benchmark-bucket-fmasz8";

/**
 * Measures the upload bandwidth of a file of the given size in MB.
 * @param {number} size The size of the file in MB.
 * @returns The upload bandwidth in MB/s.
 */
async function measureUpload(key, content) {
  const params = {
    Bucket,
    Key: key,
    Body: content.Body,
  };

  const start = new Date().getTime();
  await Promise.all(Array(10).fill(0).map(async () => await s3.upload(params).promise()));
  const end = new Date().getTime();
  const time = end - start;

  const size = content.ContentLength;
  const bandwidth = ((size * 10) * 8 / 1000000) / (time / 1000);

  return { time, bandwidth };
}

/**
 * Measures the download bandwidth of a file of the given size in MB.
 * @param {string} key The key of the file to download.
 * @returns The download bandwidth in MB/s.
 */
async function measureDownload(key) {
  const params = {
    Bucket,
    Key: key,
  };

  const start = new Date().getTime();
  await Promise.all(Array(10).fill(0).map(async () => await s3.getObject(params).promise()));
  const end = new Date().getTime();
  const time = end - start;

  const content = await s3.getObject(params).promise();
  const size = content.ContentLength;

  const bandwidth = ((size * 10) * 8 / 1000000) / (time / 1000);

  return { time, bandwidth, content };
}

module.exports.tester = async (event) => {
  const download10 = await measureDownload("10mb.txt");

  const now = Date.now();
  const upload10 = await measureUpload(`${now}/10mb.txt`, download10.content);

  delete download10.content;

  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        download10,
        upload10,
      },
      null,
      2
    ),
  };
}

module.exports.info = async (event) => {
  const cpu = await si.cpu();
  const os = await si.osInfo();
  const ram = await si.mem();

  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        cpu,
        os,
        ram,
      },
      null,
      2
    ),
  };
}