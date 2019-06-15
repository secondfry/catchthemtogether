<?php

require 'vendor/autoload.php';

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Message\ResponseInterface as Response;

class OurDB{
  private static $host = "localhost";
  private static $db_name = "ourdb_name";
  private static $username = "root";
  private static $password = "jojo";
  public static $conn = null;

  public static function getConnection(){

    try{
      OurDB::$conn = new PDO("mysql:host=" . OurDB::$host . ";dbname=" . OurDB::$db_name, OurDB::$username, OurDB::$password);
      OurDB::$conn->exec("set names utf8");
    } catch(PDOException $exception){
      echo "Connection error: " . $exception->getMessage();
    }
    return OurDB::$conn;
  }

  public static function query($select){
    if (OurDB::getConnection() == null){
      echo "Connection error";
      return;
    }
    OurDB::getConnection()->query($select);
  }
}

$c = new \Slim\Container();

$c['notFoundHandler'] = function ($c) {
  return function (Request $request, Response $response) use ($c) {
    $data = file_get_contents('index.html');
    return $response->write($data);
  };
};

//Create Slim
$app = new \Slim\App($c);

$table1 = "streamers";
$table2 = "streams";

$app->get('/api/streamers/all', function (Request $request, Response $response, array $args) {
  $res = OurDB::query('SELECT id, twitch_name, streamers FROM streamers');
  return $response->withJSON($res);
});

$app->get('api/streamers/{name}', function (Request $request, Response $response, array $args){
  $twitch_name = args['name'];
  $stream = OurDB::query('SELECT stream_name FROM streams WHERE twitch_name=' . $twitch_name);
  return $response->withJSON($stream);
});

$app->get('api/streamers/{name}/{vod_id}', function (Request $request, Response $response, array $args){
  $twitch_name = args['name'];
  $id_vod = args['vod_id'];
  return $response->withJSON($id_vod);
});
$app->run();

?>