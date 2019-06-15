<?php

require 'vendor/autoload.php';

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Message\ResponseInterface as Response;

class OurDB{
  private $host = "localhost";
  private $db_name = "ourdb_name";
  private $username = "root";
  private $password = "jojo";
  public $conn;

  public function getConnection(){
    $this->conn = null;
    try{
      $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
      $this->conn->exec("set names utf8");
    } catch(PDOException $exception){
      echo "Connection error: " . $exception->getMessage();
    }
    return $this->conn;
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
  $id->query('SELECT id FROM streamers');
  $twitch_name->query('SELECT twitch_name FROM streamers');
  $streamer->query('SELECT name FROM streamers');
  $response->getBody()->withJSON($id, $twitch_name, $streamer);
  return $response;
});

$app->get('api/streamers/{name}', function (Request $request, Response $response, array $args){
  $twitch_name = args['name'];
  $stream->query('SELECT stream_name FROM streams WHERE twitch_name=' . $twitch_name);
  $response->getBody()->withJSON($stream);
});

$app->get('api/streamers/{name}/{vod_id}', function (Request $request, Response $response, array $args){
  $twitch_name = args['name'];
  $id_vod = args['vod_id'];
  $response->getBody()->withJSON($id_vod);
});
$app->run();

?>