const fs = require('fs'); 
const csv = require('csv-parse');
const phoneUtil = require('google-libphonenumber').PhoneNumberUtil.getInstance();
const PNF = require('google-libphonenumber').PhoneNumberFormat;

const trueValues = ['yes', '1'];
const falseValues = ['no', '0', ''];

const infoSeparate = [' / ', ' /', '/ ', '/', ' , ', ' ,', ', ', ','];

const regexEmail = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

const mergeConditions = ['fullname', 'eid'];

const input = "input.csv";
const output = "output.json"

let headers = [];
let contents = [];
let result = [];

fs.createReadStream(input)
  .pipe(csv())
  .on('data', (data) => {
  	contents.push(data);
  })
  .on('end', () => {
    separateHeaders();

  	contents.forEach((row) => {
      let newRow = {};
      let addresses = [];

      //Checking each of elements in the headers and atribute him to the newRow
  		headers.forEach((header, index) => {
        if (newRow[header] === "" || newRow[header] === undefined) {
            newRow[header] = booleanCheck(row[index]);
          }else if (row[index] !== "" && row[index] !== undefined){
            newRow[header] += " , " + row[index].trim();
        }

        //Create and identify the tags
        let tags = header.split(" ");
        if (header.split(" ").length > 1) {
          if (newRow[header] !== false) {
            let contents = newRow[header].split("/");
            contents.forEach(element => {
              let address = generateAddress(element, tags)
              if (address !== "" && address !== undefined) {
                addresses.push(address);
              }
            });
          }
          console.log(newRow[header])
          delete newRow[header];
        }
  		});

      if (addresses.length > 0) {
        newRow["addresses"] = addresses;
      }

      newRow["groups"] = arrayGroup(newRow["group"]);
      delete newRow["group"];

      if (!wasMerged(newRow)) {
        result.push(newRow);
      }
  	});
    
  	fs.writeFile(output, JSON.stringify(result, null, 2), function(err, result) {});
  });
  
  function separateHeaders() {
    headers = contents[0];
    contents.shift();
  }
  
  //Check if the values are empty and if the content satisfy the elements in array:  trueValues, falseValues.
  function booleanCheck(content) {
    if (trueValues.some(value => content.trim() === value)) {
      return true;
    } else if (falseValues.some(value => content.trim() === value)) {
      return false;
    } else {
      return content.trim();
    }
  }
    
  function generateAddress(content, tags) {
    let unit = {};
    unit["address"] = getAddress(tags[0], content);
    if (unit["address"] === "" || unit["address"] === undefined) {
      return;
    }
    unit["type"] = tags[0];
    unit["tags"] = [];
    tags.forEach((element, index) => {
      if (index != 0) {
        unit["tags"].push(element);  
      }
    });
    return unit;
  }

  function getAddress(type, element){
    switch(type){
      case "phone":
        if(isValidFormat(type, element)){
          return convertPhone(element);
        }else
          return;
      case "email":
        if(isValidFormat(type, element)){
          return element;
        }else
          return;
      default:
        return element;
    }
  }

  function isValidFormat(type, content){
    if (type === "phone"){
      return !content.match(/[a-z]/i);
    }else if(type === "email"){
      let emailTest = regexEmail;
      return emailTest.test(String(content).toLowerCase());
    }
    return false;
  }
  
  function convertPhone(phone) {
    const number = phoneUtil.parseAndKeepRawInput(phone, 'BR');
    const formatNumber = phoneUtil.format(number, PNF.E164).replace('+', '');
    return formatNumber;
  }
  
  function arrayGroup(content) {
    if (content === false) {
      return [];
    }
    infoSeparate.forEach((separator) => {
      content = content.replaceAll(separator, ',');
    });
    return content.split(',');
  }

  function wasMerged(newRow) {
    for(let i = 0; i < result.length; i++) {
      if (canMerge(newRow, result[i])) {
        result[i]["groups"] = result[i]["groups"].concat(newRow["groups"]);
        result[i]["groups"] = result[i]["groups"].filter(function(item, pos) {
          return result[i]["groups"].indexOf(item) == pos;
        });
        result[i]["addresses"] = result[i]["addresses"].concat(newRow["addresses"]);
        return true;
      }
    }
    return false;
  }

  function canMerge(newRow, row) {
    for (let i = 0; i < mergeConditions.length; i++) {
      if (newRow[mergeConditions[i]] !== row[mergeConditions[i]]) {
        return false;
      }
    }
    return true;
  }



  

