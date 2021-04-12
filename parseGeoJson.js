// POINT
// - obj.features[i].geometry.type
// - obj.features[i].geometry.coordinates
// - obj.features[i].id

// EDGE
// - obj.features[i].geometry.type
// - obj.features[i].src
// - obj.features[i].tgt

const fs = require('fs');
const jsonfile = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\big graphs\\graph.json"
const jsonBxlsquare = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\big graphs\\bruxelles v1\\bruxelles_square.json"
// const json = '{"features":[{"type":"Feature","geometry":{"type":"Point","coordinates":[4.3757908,50.8162023]},"properties":{"osmId":145356,"tags":{}},"id":1}]}'
let jsongraph = fs.readFileSync(jsonBxlsquare);
const all_json = JSON.parse(jsongraph);
const features = all_json.features

console.log(features[0].geometry.type);


const filename = "D:\\Users\\Alexandre\\Desktop\\ULB\\MA2\\Memoire\\Codes\\MasterThesis\\py\\testgraph2.txt"

features.forEach(f => {
    console.log(f.geometry.type)
    
    if (f.geometry.type === "Point") {
        // v id latitude longitude
        let point = "v " + f.id + " " + f.geometry.coordinates[0] + " " + f.geometry.coordinates[1] + "\n"
        console.log(point)

        fs.appendFile(filename, point, function (err) {
            if (err) throw err;
        });
    }
    else if (f.geometry.type === "LineString") {
        // e id src tgt
        let line = "e " + f.id + " " + f.src + " " + f.tgt + "\n"
        console.log(line);

        fs.appendFile(filename, line, function (err) {
            if (err) throw err;
        });
    }
});

console.log("json -> txt ==> DONE")
  
