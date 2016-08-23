/*
var demoApp = angular.module("demoApp", []);

demoApp.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{$');
  $interpolateProvider.endSymbol('$}');
});
*/

var demoApp = angular.module("demoApp", []);

demoApp

.config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.withCredentials = true;

}])


.factory('Exchange', function($http) {
  return {
    getConversion: function () {
      return $http.get('http://localhost:8000/api/exchange/');
    }
  }
})

.controller("demoCtrl", ['$scope', 'Exchange', function($scope, Exchange) {
  Exchange.getConversion().then(function(result) {
    console.log(result.data.conversion);
    $scope.conversion = result.data.conversion;
  });
}]);
