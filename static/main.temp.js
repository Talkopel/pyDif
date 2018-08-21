(() => {
	angular.module('pyDif', ['ngMaterial'])
	.controller('pyDif', pyDifCtrl);

	function pyDifCtrl($scope) {
		$scope.bla = "sdfsdf";

		$scope.heaps = [{% for heap in heaps %}
			'{{heap}}',
		{% endfor %}]

	}
})();