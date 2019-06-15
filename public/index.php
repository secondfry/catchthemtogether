<?php

require 'vendor/autoload.php';

use Psr\Http\Message\ServerRequestInterface as Request;
use Psr\Http\Message\ResponseInterface as Response;

class OurDB {
  private static $host = "192.168.21.25";
  private static $db_name = "ourdb";
  private static $username = "root";
  private static $password = "kappa123q";
  public static $conn = null;

  public static function getConnection() {
    try {
      OurDB::$conn = new PDO("mysql:host=" . OurDB::$host . ";dbname=" . OurDB::$db_name, OurDB::$username, OurDB::$password);
      OurDB::$conn->exec("set names utf8");
    } catch (PDOException $exception) {
      echo " Connection error: " . $exception->getMessage();
    }
    return OurDB::$conn;
  }

  public static function query($select) {
    if (OurDB::getConnection() == null) {
      echo " Connection error !!";
      return;
    }
    return OurDB::getConnection()->query($select);
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
  $statement = OurDB::getConnection()->prepare("SELECT id, twitch_name, name FROM streamers");
  $statement->execute();
  $results = $statement->fetchAll(PDO::FETCH_ASSOC);
  
  return $response->withJSON($results);
});

$app->get('/api/streamers/{name}', function (Request $request, Response $response, array $args) {
  $twitch_name = $args['name'];

  $statement = OurDB::getConnection()->prepare('SELECT id_vod FROM streams WHERE twitch_name = ?');
  $statement->execute(array($twitch_name));
  $results = $statement->fetchAll(PDO::FETCH_ASSOC);
  $i = 0;
  foreach($results as $result) {
    $statement = OurDB::getConnection()->prepare('SELECT twitch_name, timestamp_start, timestamp_finish FROM streams WHERE id_vod = ?');
    $statement->execute(array($result['id_vod']));

    $a[$i]['vod_id'] = $result['id_vod'];
    $a[$i]['people'] = $statement->fetchAll(PDO::FETCH_ASSOC);
    $i++;
  }
  return $response->withJSON($a);
});

$app->run();

?>