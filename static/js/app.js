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

demoApp.controller("demoCtrl", ['$scope', function($scope) {
  $scope.username = "tom";
}]);
