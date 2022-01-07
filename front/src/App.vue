<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
localStorage.setItem("flag", "false");
localStorage.setItem("backend_host", "10.176.64.134:8000");
// localStorage.setItem("backend_host", "localhost:8000");
</script>

<style>
</style>
