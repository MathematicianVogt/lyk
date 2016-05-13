(function () {
	
	var article = angular.module('article', ['overlay']);
	
	article.controller('article_controller', ['$scope', '$http', 'articles', function ($scope, $http, articles) {
		
		$scope.article = {
			init: function () {
				
				$scope.$watch(function () { return articles.articles }, $scope.article.new_article);
				
			},
			new_article: function () {
				
				article = articles.articles[$scope.n];
				
				if (!article) return; 
				
				$scope.article.id = article._id;
				$scope.article.headline = article.title;
				$scope.article.img = article.thumb;
				$scope.article.url = article.article_url;
				$scope.article.lykes = article.likes;
				$scope.article.dislykes = article.dislikes;
				
			},
			id: '',
			headline: "A Headline ryan is the greatest programmer in the world, Nobel Organization says",
			img: "http://i.imgur.com/yKpJaQr.png",
			url: "http://www.google.com",
			lykes: 1337,
			dislykes: 69,
			lyke: function () {
				$scope.article.lykes++;
				$http.get('/lyke/' + $scope.article.id);
			},
			dislyke: function () {
				$http.get('/dislyke/' + $scope.article.id);
				$scope.article.dislykes++;
			},
			overlay: {
				display: false,
				mouseover : function () {
					$scope.article.overlay.display = true;
				},
				mouseout: function () {
					$scope.article.overlay.display = false;
				}
			}
		}
		
		$scope.article.init();
		
	}]);
	
	article.directive('lykArticle', [function () {
		
		return {
			restrict: 'E',
			templateUrl: '/static/modules/article/article.html',
			controller: 'article_controller',
			scope: {
				n: '='
			}
		};
		
	}]);
	
})();