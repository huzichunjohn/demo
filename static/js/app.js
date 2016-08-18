/*
var demoApp = angular.module("demoApp", []);

demoApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});
*/

var demoApp = angular.module("demoApp", [], function($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

demoApp.controller("demoCtrl", ['$scope', '$http', function($scope, $http) {
  /*
  $scope.posts = [{"author": {"username": "joe"}, "title": "sample post #1", "body": "this is the first sample post"},
    {"author": {"username": "karen"}, "title": "sample post #2", "body": "this is another sample post"}];
  */
  $scope.todos = [];
  $http.get("/api/todos/").then(function(result) {
    console.log(result.data.results);
    result.data.results.forEach(function(val, i) {
      $scope.todos.push({"todo": val["todo"], "timestamp": val["timestamp"], "completed": val["completed"], "priority": val["priority"]});
    });
  });

}]);
