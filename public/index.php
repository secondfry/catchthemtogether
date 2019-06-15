<?php

require 'vendor/autoload.php';

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Message\ResponseInterface as Response;

$c = new \Slim\Container();

$c['notFoundHandler'] = function ($c) {
  return function (Request $request, Response $response) use ($c) {
    $data = file_get_contents('index.html');
    return $response->write($data);
  };
};

//Create Slim
$app = new \Slim\App($c);

$app->get('/api/', function (Request $request, Response $response, array $args) {
  $response->getBody()->write("Hello, world!");
  return $response;
});

$app->run();
