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

  await s3.upload(params).promise();

  const end = new Date().getTime();
  const time = end - start;
  const size = content.ContentLength;

  const bandwidth = (size * 8 / 1000000) / (time / 1000);

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

  const content = await s3.getObject(params).promise();

  const end = new Date().getTime();
  const time = end - start;
  const size = content.ContentLength;

  const bandwidth = (size * 8 / 1000000) / (time / 1000);

  return { time, bandwidth, content };
}

module.exports.tester = async (event) => {
  const download10 = await measureDownload("10mb.txt");
  const download100 = await measureDownload("100mb.txt");

  const now = Date.now();
  const upload10 = await measureUpload(`${now}/10mb.txt`, download10.content);
  const upload100 = await measureUpload(`${now}/100mb.txt`, download100.content);

  delete download10.content;
  delete download100.content;

  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        download10,
        download100,
        upload10,
        upload100,
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