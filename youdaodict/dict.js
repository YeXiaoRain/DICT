#!/usr/bin/env node
"use strict";

const argv     = require("process").argv;
const youdaodict = require("./youdaodict");

var queryWord = argv.slice(2).join(" ");

function debug(){
  var testDict = new youdaodict();
  testDict.trans(queryWord);
}
debug();
