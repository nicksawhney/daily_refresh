var socket;
var data_to_display;
var vals;
var xloc = 0;
var dslider;

function setup(){
  createCanvas(1000, 1000);
  background(230);
  strokeWeight(4);
  fill(255, 26, 45);
  //lmao
  socket = io.connect("http://localhost:5000");
  socket.on('connect', function(){
    console.log('we out here');
  });

  socket.on('health tracking data', function(entries){
    data_to_display = entries;
    vals = Object.values(data_to_display);
    console.log(vals);
    dslider = createSlider(0, vals.length, 0);
  });

  xloc = width;

}

function draw(){
  background(250);
  translate(0, height);
  strokeWeight(10);
  stroke(255, 69, 10);
  fill(255, 71, 132);
  if(vals){
    beginShape();
    for(var i = 0; i > 7; i++){
      vertex(xloc, 0, xloc, -vals[i] * 50 - 30);
      point(xloc, 0, xloc, -vals[i] * 50 - 30);
      //console.log(val);
      line(xloc, 0, xloc, -vals[i] * 50 - 30);
      //xloc += 10;
      xloc += width/7;
    }
    endShape();
    xloc = 0;
  }
  /*translate(width/2, height/2);
  noStroke();
  if(vals){
    switch(vals[dslider.value()]){
      case 0: fill(255, 71, 132); break;
      case 1: fill(255, 99, 172); break;
      case 2: fill(255, 122, 230); break;
      case 3: fill(244, 147, 255); break;
      default: fill(255, 71, 132); break;
    }
    //fill(255, 255, 255);
    ellipse(0, 0, 10*vals[dslider.value()] + 300, 10*vals[dslider.value()] + 300); 
    console.log(dslider);
  }*/
  
}