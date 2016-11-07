[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6a480c4abec04cfa94dac28245f23c61)](https://www.codacy.com/app/arnold-okoth/cp2_blapi?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-aokoth/cp2_blapi&amp;utm_campaign=Badge_Grade)

# BucketList API

## Introduction

> This application is a Flask API for a bucket list service that allows users to create, update and delete bucket lists. It also provides programmatic access to the items added to the items created. This API is a REST API and the return format for all endpoints is JSON.

## Endpoints

1. `POST /auth/login`
2. `POST /auth/register`
3. `GET /bucketlists/`: returns all bucket listing of all buckets list
4. `GET /bucketlists/<id>`: returns the bucket list with the specified ID
5. `PUT /bucketlist/<id>`: updates the bucket list with the specified with the provided data
6. `DELETE /bucketlist/<id>`: deletes the bucket list with the specified ID
7. `POST /bucketlists/<id>/items/`: adds a new item to the bucket list with the specified ID
8. `PUT /bucketlists/<id>/items/<item_id>`: updates the item with the given item ID from the bucket list with the provided ID
9. `DELETE /bucketlists/<id>/items/<item_id>`: deletes the item with the specified item ID from the bucket list with the provided ID
