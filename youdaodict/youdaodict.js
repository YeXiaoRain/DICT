#! /usr/bin/env node
const request  = require("request");
const chalk    = require("chalk");

module.exports = class youdaodict{
  constructor() { 
    this.url  = 'http://fanyi.youdao.com/openapi.do?keyfrom=prettygirl22&key=69628370&type=data&doctype=json&version=1.1&q=';
  }
  doPrint(body){
    console.log(`${chalk.yellow('翻译')}: ${chalk.cyan(body.translation[0])}`);
    if (body.basic) {
      let basic = body.basic;
      let us = basic['us-phonetic'] ? `; 美式 [ ${basic['us-phonetic']} ]` : '';
      console.log(`${chalk.yellow('发音')}: ${chalk.cyan('[ ' + basic.phonetic + ' ]')} ${chalk.magenta(us)}`);
      console.log(chalk.yellow(`释义:`));
      basic.explains.forEach((item, index) => {
        console.log(`  ${index+1}. ${chalk.cyan(item)}`);
      });
      // console.log(`${chalk.yellow('发音')} ${chalk.grey('-')} ${chalk.cyan(basic.phonetic)}`);
    } 
    if (body.web) {
      let web = body.web;
      console.log(chalk.yellow(`其他: `));
      web.forEach((item, index) => {
        let header = `  ${index+1}. ${item.key}`;
        console.log((header));
        console.log('    ' + chalk.cyan(item.value.toString()));
      });
    }
  }
  trans(queryString){
    var q = encodeURIComponent(queryString);
    request(this.url + q, (err, res, body) => {
      if (err) {
        console.log('error:' + err);
      }
      this.doPrint(JSON.parse(body));
    });
  }
}
