(function () {
	
	var overlay = angular.module('overlay', []);
	
	overlay.controller('overlay_controller', ['$scope', function ($scope) {
		
		$scope.overlay = {
			init: function () {}
		}
		
		$scope.article.init()
		
	}]);
	
	overlay.directive('lykOverlay', [function () {
		
		return {
			restrict: 'E',
			templateUrl: '/static/modules/overlay/overlay.html',
			controller: 'overlay_controller'
		};
		
	}]);
	
})();