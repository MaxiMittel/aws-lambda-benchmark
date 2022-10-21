"use strict";
const AWS = require("aws-sdk");
const s3 = new AWS.S3();
const si = require("systeminformation");
const Bucket = "aws-lambda-benchmark-bucket-fmasz8";
const TEST_SIZE = 100;

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

  const totalStart = new Date().getTime();
  const times = await Promise.all(Array(TEST_SIZE).fill(0).map(async () => {
    const start = new Date().getTime();
    await s3.upload(params).promise();
    const end = new Date().getTime();
    return end - start;
  }));
  const totalEnd = new Date().getTime();
  const totalTime = totalEnd - totalStart;

  const size = content.ContentLength;

  return {
    total: {
      time: totalTime,
      bandwidth: ((size * TEST_SIZE) * 8 / 1000000) / (totalTime / 1000),
    },
    times,
    bandwidth: times.map(t => (size * 8 / 1000000) / (t / 1000)),
  };
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

  const totalStart = new Date().getTime();
  const times = await Promise.all(Array(TEST_SIZE).fill(0).map(async () => {
    const start = new Date().getTime();
    await s3.getObject(params).promise();
    const end = new Date().getTime();
    return end - start;
  }));
  const totalEnd = new Date().getTime();
  const totalTime = totalEnd - totalStart;

  const content = await s3.getObject(params).promise();
  const size = content.ContentLength;

  return {
    total: {
      time: totalTime,
      bandwidth: ((size * TEST_SIZE) * 8 / 1000000) / (totalTime / 1000),
    },
    times,
    bandwidth: times.map(t => (size * 8 / 1000000) / (t / 1000)),
    content,
  };
}

module.exports.tester = async (event) => {
  const download = await measureDownload("10mb.txt");

  const now = Date.now();
  const upload = await measureUpload(`${now}/10mb.txt`, download.content);

  delete download.content;

  return {
    statusCode: 200,
    body: JSON.stringify(
      {
        download,
        upload,
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