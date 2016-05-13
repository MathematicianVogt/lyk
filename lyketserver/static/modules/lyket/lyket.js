(function() {

	var lyket = angular.module('lyket', ['article']);

	lyket.factory('articles', function() {

		return {
			articles: []
		};

	});

	lyket.controller('lyket_controller', ['$scope', '$http', 'articles',
		function($scope, $http, articles) {

			$scope.articles = function() {

				$http.get('/articles')
					.success(function(data) {

						articles.articles = data.results;

					})
					.error(function(error) {
						console.log('We got fucked: ' + error);
					});

			};
			$scope.articles();

		}
	]);

})();
