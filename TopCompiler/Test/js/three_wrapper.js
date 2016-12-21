var THREE = require("three");
var Stats = require("stats.js");

var stats = new Stats()
stats.showPanel( 0 ); // 0: fps, 1: ms, 2: mb, 3+: custom
document.body.appendChild( stats.dom );

window.th_scene = function th_scene(mesh) {
    var scene = new THREE.Scene()

    for (var i = 0; i < mesh.length; i++) {
        scene.add(mesh.get(i));
    }
    return scene
}

window.th_perspectiveCamera = function th_perspectiveCamera(a,b,c,d, attributes) {
    return set(new THREE.PerspectiveCamera(a,b,c,d), attributes);
}

function toThreeObject(defered) {
    var Something = defered.name

    function F(args) {
        return Something.apply(this, args);
    }
    F.prototype = Something.prototype;


    return new F(defered.args);
}

function patch(lastV, newV, scene, camera) {
    var lastVCamera = lastV.camera
    var lastVScene = lastV.scene

    var newVCamera = newV.camera
    var newVScene = newV.scene

    function patchMesh(mesh, last, current) {
        var attributes = current.args;
        var lastMap = toObject(last.args)

        for (var i = 0; i < attributes.length; i++) {
            var attr = attributes.get(i);

            var names = attr.name.split(".")
            var part = mesh;
            for (var c = 0; c < names.length-1; c++) {
                part = part[names[c]];
            }

            if (attr.value.args !== undefined) {
                var res = func(lastMap[attr.name], attr.value, part[names[c]]
           
                part[names[c]] = func(lastMap[attr.name], attr.value, part[names[c]]
            } else {
                part[names[c]] = attr.value;
            }
        }
        return mesh;
    }

    function func(last, current, object) {
        if (last.name !== current.name || last.args.length > current.args.length) {
            return toThreeObject(current);
        }

        return patchMesh(object, last, current);
    }

    func(scene, lastVScene, currentVScene);
    func(camera, lastVCamera, currentVCamera);
}

window.th_init = function th_init(name) {
    var renderer = new THREE.WebGLRenderer(name);
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.getElementById(name).appendChild(renderer.domElement);

    return renderer
}

window.th = THREE;

window.th_constructor = function th_constructor(Something) {
    function F(args) {
        return Something.apply(this, args);
    }
    F.prototype = Something.prototype;

    return function() {
        return new F(arguments);
    }
}

function set(mesh, attributes) {
    for (var i = 0; i < attributes.length; i++) {
        var attr = attributes.get(i);

        var names = attr.name.split(".")
        var part = mesh;
        for (var c = 0; c < names.length-1; c++) {
            part = part[names[c]]
        }
        part[names[c]] = attr.value;
    }
    return mesh;
}

window.th_combineMeshes = function th_combineMeshes(meshes, attributes) {
    var l = meshes.length;
    var newMesh = new THREE.Object3D()

    for (var i = 0; i < l; i++) {
        newMesh.add(meshes.get(i));
    }

    return set(newMesh, attributes);
}

window.th_mesh = function th_mesh(geom, material, attributes) {
    //console.log(material);
    return set(new THREE.Mesh(geom, material), attributes);
}

window.th_render = function th_render(renderer, scene, camera, callback) {
    renderer.render(scene, camera)
    callback()
}

window.th_toObject = function th_toObject(attr) {
    var obj = {};
    for (var i = 0; i < attr.length; i++) {
        var a = attr.get(i);
        obj[a.name] = a.value;
    }

    return obj;
}





window.th_meshPhongMaterial = function th_meshPhongMaterial(attributes) {
    //console.log();
    var t = new THREE.MeshPhongMaterial(th_toObject(attributes));
    //console.log(t);
    return t;
}



window.th_hemisphereLight = function th_hemisphereLight(a,b,c, attributes) {
    var hemiLight = new THREE.HemisphereLight(a, b, c );
    return set(hemiLight, attributes);
}

window.th_fps = function th_fps(update, maxFPS, view) {
    var nextF = function () {
        stats.end()
        requestAnimationFrame(fps);
    }
    var newView = function () {
        view(nextF);
    }
    var lastFrameTimeMs = 0;
    function fps(timestamp) {
        stats.begin()
        update(timestamp-lastFrameTimeMs, newView)
        lastFrameTimeMs = timestamp;
    }
    requestAnimationFrame(fps);
}

/*
window.th_fps = function core_fps(update, maxFPS, view) {
    var timestep = 1000 / maxFPS;
    var delta = 0;
    var lastFrameTimeMs = 0;

    function _fps(timestamp) {
        if (timestamp < lastFrameTimeMs + (1000 / maxFPS)) {
            requestAnimationFrame(_fps);
            return
        }

        stats.begin()

        if (timestamp-lastFrameTimeMs > 10*timestep) {
            delta = 0
            lastFrameTimeMs = timestamp;
            requestAnimationFrame(_fps);

            return
        }

        // Track the accumulated time that hasn't been simulated yet
        delta += timestamp - lastFrameTimeMs; // note += here
        lastFrameTimeMs = timestamp;

        // Simulate the total elapsed time in fixed-size chunks
        function func() {
            if (delta >= timestep) {
                update(timestep, func);
                delta -= timestep;
            } else {
                requestAnimationFrame(_fps);
            }
        }



        view(func);

        stats.end()
    }
    requestAnimationFrame(_fps);
}
*/

