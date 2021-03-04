
// POINT
// - obj.features[i].geometry.type
// - obj.features[i].geometry.coordinates
// - obj.features[i].id

// EDGE
// - obj.features[i].geometry.type
// - obj.features[i].src
// - obj.features[i].tgt

const json = '{"features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[4.3757908,50.8162023]},"properties":{"osmId":145356,"tags":{}},"id":1}]}'
const obj = JSON.parse(json);

console.log(obj.features[0].geometry.type);

const fs = require('fs');
const filename = "D:\Users\Alexandre\Desktop\ULB\MA2\Memoire\Codes\graph.txt"

obj.features.forEach(function (f) {
    console.log(feature.type);
    
    if (f.geometry.type == "Point") {
        // v id latitude longitude
        console.log("v " + f.id + " " + f.geometry.coordinates[0] + " " + f.geometry.coordinates[1])
        fs.writeFile(filename, "v " + f.id + " " + f.geometry.coordinates[0] + " " + f.geometry.coordinates[1]);
    }
    else if (f.geometry.type == "LineString") {
        // e id src tgt
        console.log("e " + f.id + " " + f.src + " " + f.tgt);
        fs.writeFile(filename, "e " + f.id + " " + f.src + " " + f.tgt);
    } 
});
  
