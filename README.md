# Introduction

This is a OrderManagement application that is very generic. You don't need to write complicated Serializers and Views if
not really necessary. This project used GenericModelSerializers and GenericApiViews

## Installation and Deploying

Basically, docker will install and deploy everything, you don't need extra efford.

    docker-compose up

If you add new libraries into django, you should build Dockerfile again.


## How to Use

You can find Yemeksepeti.json file in directory.

- import the file into Postman
- register users (under Auth folder. You can check examples)
- to access endpoint under Serve either register with admin@admin.com or change username from environment with valid
  user
- before create an order; restaurant, categories and food need to be created
- all the endpoints with example can be found under Serve folder.
- call services below, respectively. You can find example in postman documentation
  - [POST] /serve/restaurant/
  - [POST] /serve/category/
  - [POST] /serve/food/
  
  ###**!! On the other hand, you can simply send serve/order/generate_test_data/ to create dummy restaurants, categories and foods, after you created 3 users !!**
- websocket connection need to be opened, otherwise, order cannot be created. To do that you can copy/paste the following command into 
Postman (it is not supported by POSTMAN)

      {{WS_PROTOCOL}}//{{SERVER_HOST}}:{{WS_PORT}}/ws/order/<restaurant_id>/?&token=<token>
      
      Example: ws://localhost:8001/ws/order/1/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluQGFkbWluLmNvbSIsImV4cCI6MTYzNzk2MTA3Mn0.H_5hdxI_E33v3MahBlpE3LzT4PFLjef91IPPDoKd1jw

- After that, when someone created an order, it will be published on Channel and will be visible in Chat.
- After you see the new order, the status of order will change QUEUED to RUNNING
- To complete order, you can use complete order endpoint under Serve folder
  - [POST] /serve/order/complete/ with food_id
- Order status can be seen in [GET] /serve/order/. This endpoint shows all order status. If you want to see 
login users order, you need to use /serve/order/list_by_user, an example can be found in Serve folder.
-  list_by_user can be used for food, restaurant and order. Example: [GET] /serve/food/list_by_user , [GET] /serve/restaurant/list_by_user 

## Flush Databases
If need, you should delete volume to flush database by following command:
    
    docker compose down
    docker volume prune

or you can connect to container:
    
    docker ps
    docker exec -ti <container_id_of_ordermanagement_app_image> bash
    python manage.py flush
    

## Future Works

- Before publish order, it can be checked whether restaurant is online or not.
- DB column can be reconsidered. More efficient ways need search   
- Unittest can be complete, factory functions need to be defined for ws

## Future Database Tables

If you want to add services which just need create, list and retrieve, you can define in OrderManagement/config.py after
you create model.

## Test

Test will be run when you run

    docker compose up

But, if you want to test it seperately, you can list of container by

    docker ps
    docker exec -ti <container_id_of_ordermanagement_app_image> bash
    python manage.py test