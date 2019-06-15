<template>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <router-link to="/" class="navbar-brand">21 FRY FRY</router-link>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
	  	<router-link to="/" class="nav-link" activeClass="active">Home</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/list" class="nav-link" activeClass="active">List</router-link>
      </li>
    </ul>
  </div>
</nav>
</template>