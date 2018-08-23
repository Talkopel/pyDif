(() => {
	angular.module('pyDif', ['ngMaterial'])
	.controller('pyDif', pyDifCtrl);

	rawHeaps = {
		{% for heap in heaps %}
		'{{ heap }}': {{ parsed_heaps_and_chunks[heap]}},
		{% endfor %}
	}


	function pyDifCtrl($scope) {
		$scope.bla = "sdfsdf";

		$scope.heapSearch = {
			'notZeroed': false,
			'greaterThan': 0,
			'lessThan': 10000000,
			'withString': '',
		}
		$scope.heaps = Object.keys(rawHeaps);


		$scope.fetch = function(heap) {

			$scope.blocks = rawHeaps[heap].filter((block) => {
				if (block.meta_blockSize < $scope.heapSearch.lessThan &&
					block.meta_blockSize > $scope.heapSearch.greaterThan &&
					emptyChunk(block.meta_data) == $scope.heapSearch.notZeroed) return true;
			})

			console.log($scope.blocks);

		}


		function emptyChunk(meta_data) {
			for (let i = 0; i < meta_data.length; i++) {
				if (meta_data[i] != 0) return false;
			}
			return true;
		}


	}


})();