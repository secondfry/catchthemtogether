<script>

import LayoutDefault from '../layout/default.vue';
import Navigation from '../layout/nav.vue';
import '../../scss/root.scss';
import '../../scss/nav.scss';


export default {
  components: {
    LayoutDefault,
	Navigation
  }
}


</script>

<template>
<layout-default>
	<navigation></navigation>
	<div class="container">
		<div class="row">
			<div class="col bg-light justify-content-center main">
				<h1 class="text-center">Хакатон 21</h1>
			</div>
		</div>
	</div>
</layout-default>
</template>