<script>

import LayoutDefault from '../layout/default.vue';
import Navigation from '../layout/nav.vue';
import '../../scss/list.scss';
import '../../scss/nav.scss';
// import pic from  '../../ads/w.png';

export default {
  components: {
    LayoutDefault,
	Navigation
  }
}
</script>

<template>
<layout-default class="bg">
	<navigation></navigation>
	<div class="row">
		<div class="col-12 col-md-0 col-lg-2"></div>
		<div class="col-12 col-md-8 col-lg-8 bg-light">
			<div class="row">Top #1</div>
			<div class="row">Top #2</div>
			<div class="row">Top #3</div>
			<div class="row">Top #4</div>
			<div class="row">Top #5</div>
			<div class="row">Top #6</div>
			<div class="row">Top #7</div>
			<div class="row">Top #8</div>
			<div class="row">Top #9</div>
			<div class="row">Top #10</div>
			<div class="row">Top #11</div>
			<div class="row">Top #12</div>
		</div>
		<div class="col-8 col-md-4 col-lg-2">
			<div style='position: relative;'>
				<img class='img-fluid' src="../../ads/w.png">
				<div class='ad-text'>Play wolf 3d online for free!!!</div>
			</div>
		</div>
	</div>
</layout-default>
</template>