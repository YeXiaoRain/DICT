#!/usr/bin/env node
"use strict";

const got = require('got')
const yargs = require('yargs')
const cheerio = require('cheerio')
const colors = require('colors')
const _ = require('lodash')

module.exports = class bingdict {
  constructor() {
    this.bingUrl = "http://cn.bing.com/dict/search?mkt=zh-cn&q=";

    this.color = function(index,text){
      if(_.isUndefined(text)){
        return "";
      }else{
        return this.colorOn[index](text);
      }
    }
    this.colorOn=[];
    this.colorOn[0] = function(text){return text.white.bgBlack.bold;}
    this.colorOn[1] = function(text){return text.rainbow.bold.underline;}
    this.colorOn[2] = function(text){return text.rainbow;}
    this.colorOn[3] = function(text){return text.white;}
    this.colorOn[4] = function(text){return text.black.bgWhite;}
  }

  trans(query){
    query = encodeURIComponent(query);
    got(this.bingUrl + `${query}`).then(response => {
      var formedString = this.formatResponse(response);
      console.log(formedString);
    })
    .catch(error => {
      console.log(error)// TODO: Handle error
    })
  }

  formatResponse(queryResponse) {
    var returnArray = [];
    var $ = cheerio.load(queryResponse.body);

    returnArray.push('\n' + this.color(0,$('.hd_pr').text()));//pron_en
    returnArray.push('\n' + this.color(1,$('.qdef ul li').eq(0).find('.pos').text().toUpperCase() + ' ' + $('.qdef ul li').eq(0).find('.def').text()));//dict_trans
    returnArray.push('\n' + this.color(2,$('.qdef ul li').eq(1).find('.pos').text().toUpperCase() + ' ' + $('.qdef ul li').eq(1).find('.def').text()));//net_trans
    var crossid=[];
    $('#crossid .def_fl').children(' .de_li1').each(function () {
      crossid.push($(this).text());
    });
    returnArray.push('\n'+this.color(3,crossid.join('\n')));
    var homoid=[];
    $('#homoid .def_fl').children(' .de_li1').each(function () {
      homoid.push($(this).text());
    });
    returnArray.push('\n'+this.color(4,homoid.join('\n'))); 
    return returnArray.join('');
  }
}
