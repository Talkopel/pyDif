(() => {
	angular.module('pyDif', ['ngMaterial'])
	.controller('pyDif', pyDifCtrl);

	function pyDifCtrl($scope) {
		$scope.bla = "sdfsdf";

		$scope.heaps = [ {% for heap in heaps %} '{{heap}}', {% endfor %} ]
		$scope.data_heaps = { {% for heap in heaps %}
			'{{heap}}': {{ parsed_heaps_and_chunks[heap] }},
		{% endfor %} }

		console.log($scope.data_heaps[heaps[0]].length)
	}


})();