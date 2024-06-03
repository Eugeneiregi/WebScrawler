function program(input){
  var output = 0;
  if (input[0] == "add") {
    output = add();
  } else if (input[0] == "charge"){
    output = charge(); 
  } else {
    output = credit();
  }

  return outuput;
}

function add(){
  return 0;
}

function charge(){
  return 0;
}

function credit(){
  return 0;
}

// TODO: Research on ways to read and write to and from the console in javascript.
// Add functionality to add, charge, and credit
// Review program
// Add functionality to read a file using program
