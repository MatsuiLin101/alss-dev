String.prototype.format = function() {
  a = this;
  for (k in arguments) {
    a = a.replace("{" + k + "}", arguments[k])
  }
  return a
}

function numberWithCommas(num){
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
}


