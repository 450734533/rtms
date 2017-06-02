<template>
    <div class="op-badge"><slot></slot></div>
</template>

<style scoped>
  .op-badge {
    position: absolute;
    top: -10px;
    right: -22px;
    display: inline-block;
    padding: 2px 5px;
    background-color: #f30;
    border-radius: 3px;
    font-size: 12px;
    color: #fff;
    line-height: 1;
  }

  .op-badge:before {
    position: absolute;
    content: '';
    color: #f30;
    bottom: -5px;
    left: 50%;
    margin-left: -4px;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 5px 4px 0 0;
    border-color: #ff3300 transparent transparent transparent;
  }
</style>