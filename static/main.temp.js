(() => {
	angular.module('pyDif', ['ngMaterial'])
	.controller('pyDif', pyDifCtrl);

	rawHeaps = {
		{% for heap in heaps %}
		{{ heap }}: '{{ parsed_heaps_and_chunks[heap]}}',
		{% endfor %}
	}

	function pyDifCtrl($scope) {
		$scope.bla = "sdfsdf";

		$scope.heapIds = Object.keys(rawHeaps);
	}


})();