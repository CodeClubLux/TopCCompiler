var THREE = require("three");
var CANNON = require("cannon");

var Stats = require("stats.js");

window.th_scene = function th_scene(mesh) {
    return {name: THREE.Scene, args: mesh.map(function(i, idx) {
        return {name: "children."+idx, value: i}
    })}
}

window.th_perspectiveCamera = function th_perspectiveCamera(a,b,c,d, attributes) {
    return {name: THREE.PerspectiveCamera,
        args: attributes
            .append({name: "fov", value: a})
            .append({name: "aspect", value: b})
            .append({name: "near", value: c})
            .append({name: "far", value: d})
    }
}

window.th_toThreeObject = function th_toThreeObject(defered) {
    var Something = defered.name

    var args = defered.args
    if (Something === THREE.Mesh) {
        var a = args.get(args.length-2).value
        var b = args.get(args.length-1).value
        return set(new Something(th_toThreeObject(a), th_toThreeObject(b)), args, args.length-2);
    } else if (Something === THREE.SphereGeometry || Something === THREE.BoxGeometry) {
        var a = args.get(args.length-3).value
        var b = args.get(args.length-2).value
        var c = args.get(args.length-1).value
        return new Something(a, b, c)
    } else if (Something === CANNON.World) {
        var world = new CANNON.World()
        for (var i = 0; i < args.length-1; i++) {
            world.addBody(th_toThreeObject(args.get(i).value));
        }
        var g = args.get(-1).value
        world.gravity.set(g.x, g.y, g.z);
        return world;
    }

    return set(new Something(),
        defered.args.map(function (x) {
            return ({
                name: x.name,
                value: (x.value.args !== undefined ? th_toThreeObject(x.value) : x.value)
            })
        })
    );
}
function th_patchMesh(mesh, last, current) {
        var attributes = current.args;
        var lastMap = th_toObject(last.args)

        for (var i = 0; i < attributes.length; i++) {
            var attr = attributes.get(i);

            var names = attr.name.split(".")
            var part = mesh;
            for (var c = 0; c < names.length-1; c++) {
                if (names[c] === "children") {
                    attr.value.parent = mesh;
                } else if (names[c] === "bodies") {
                    //console.log("bodies" + names[c+1]);
                    if (names[c+1] >= mesh.bodies.length) {
                        //console.log("adding body");
                        return mesh.addBody(attr.value);
                    }
                    attr.value.world = mesh;
                }
                part = part[names[c]];
            }

            if (attr.value.args !== undefined) {
                var res = func(lastMap[attr.name], attr.value, part[names[c]])

                part[names[c]] = res;
            } else {
                switch (names[c]) {
                case "color":
                    part.color.setHex(attr.value);
                    break
                case "groundColor":
                    part.groundColor.setHex(attr.value);
                    break
                case "gravity":
                    console.log(part);
                    part.setGravity(attr.value);
                    break;
                default:
                    part[names[c]] = attr.value;
                }
            }
        }
        return mesh;
    }

function func(last, current, object) {
    if (last.name !== current.name || last.args.length > current.args.length) {
        return th_toThreeObject(current);
    }

    return th_patchMesh(object, last, current);
}

window.th_box = function th_box(x,y,z) {
    return new CANNON.Box(new CANNON.Vec3(x,y,z));
}

window.th_sphere = function th_circle(radius) {
    return new CANNON.Sphere(radius);
}

window.th_plane = function th_plane() {
    return new CANNON.Plane()
}

window.th_body = function th_body(attributes) {
    return new CANNON.Body(th_toObject(attributes));

    return {name: CANNON.Body, args: attributes}
}

window.th_vec3 = function vec3(x,y,z) {
    return new CANNON.Vec3(x,y,z);
}

window.th_world = function th_world(gravity) {
    var w = new CANNON.World();
    w.gravity.set(gravity.x, gravity.y, gravity.z);
    return w;

    return {name: CANNON.World, args: newVector({name: "gravity", value: gravity})}
}

window.th_physics = function th_physics() {
    var timestep = 1.0/60;
    var oldWorld;
    var realMeshes = false;
    function simulation(world, meshes, delta, steps) {
        if (!realMeshes) {
            for (var i = 0; i < meshes.length; i++) {
                console.log(meshes.get(i));
                world.addBody(meshes.get(i));
            }
            realMeshes = world;
            console.log(world);
            realMeshes.step(timestep, delta/1000, steps);
            return fromArray(realMeshes.bodies);
        } else {
            realMeshes.step(timestep, delta/1000, steps);
            return fromArray(realMeshes.bodies);
        }


        meshes = meshes.map(function(i, idx) {
            return {name: "bodies."+idx, value: i}
        })

        var newWorld = {name: world.name, args: meshes.operator_add(world.args)}

        if (!realMeshes) {
            realMeshes = th_toThreeObject(newWorld);
            realMeshes.step(timestep, delta/1000, steps);
            oldWorld = newWorld;
            console.log(realMeshes);
            return fromArray(realMeshes.bodies);
        } else {
            realMeshes.step(timestep, delta/1000, steps);
            return fromArray(realMeshes.bodies);
        }

        realMeshes = func(oldWorld, newWorld, realMeshes);

        realMeshes.step(timestep, delta, steps);

        oldWorld = newWorld;

        //var res = fromArray(realMeshes.bodies);
        return fromArray(realMeshes.bodies);
    }

    return simulation;
}


window.th_patch = function th_patch(lastV, newV, scene, camera) {
    var lastVCamera = lastV[1];
    var lastVScene = lastV[0];

    var currentVCamera = newV[1];
    var currentVScene = newV[0];



    var scene = func(lastVScene, currentVScene, scene);
    var camera = func(lastVCamera, currentVCamera, camera);
    return [scene, camera]
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

function set(mesh, attributes, length) {
    length = length || attributes.length
    loop1:
        for (var i = 0; i < length; i++) {
            var attr = attributes.get(i);

            var names = attr.name.split(".")
            var part = mesh;

            for (var c = 0; c < names.length-1; c++) {
                if (names[c] === "children") {
                    //mesh.add(attr.value)
                    //continue loop1;
                    attr.value.parent = mesh;
                }
                part = part[names[c]]
            }
            switch (names[c]) {
            case "color":
                part.color.setHex(attr.value);
                break
            case "groundColor":
                part.groundColor.setHex(attr.value);
                break
            case "shape":
                part.addShape(attr.value);
                break
            case "gravity":
                console.log(part);
                part.gravity.set(attr.value);
                break
            default:
                part[names[c]] = attr.value;
            }

        }

    return mesh;
}

window.th_combineMeshes = function th_combineMeshes(meshes, attributes) {
    var l = meshes.length;

    return {
        name: THREE.Object3D,
        args: attributes.operator_add(meshes.map(function (i, idx) { return {name: "children."+idx, value: i}}))
    }
}

window.th_mesh = function th_mesh(geom, material, attributes) {
    //console.log(material);
    return {
        name: THREE.Mesh,
        args: attributes.append({name: "geometry", value: geom}).append({name: "material", value: material})
    }
}

window.th_render = function th_render(renderer, scene, camera, callback) {
    //renderer.setClearColor(0xEEEEEE);
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
    return {name: THREE.MeshPhongMaterial, args: attributes};
}

window.th_BoxGeometry = function th_BoxGeometry(a,b,c) {
    return {name: THREE.BoxGeometry, args: newVector(
        {name: "parameters.width", value: a},
        {name: "parameters.height", value: b},
        {name: "parameters.depth", value: c}
    )};
}

window.th_SphereGeometry = function th_BoxGeometry(a,b,c) {
    return {name: THREE.SphereGeometry, args: newVector(
        {name: "parameters.radius", value: a},
        {name: "parameters.widthSegments", value: b},
        {name: "parameters.heightSegments", value: c}
    )};
}

window.th_hemisphereLight = function th_hemisphereLight(a,b,c, attributes) {
    var hemiLight = {name: THREE.HemisphereLight, args: attributes
        .append({name: "color", value: a})
        .append({name: "groundColor", value: b})
        .append({name: "intensity", value: c})
    }
    return hemiLight;
}

window.th_fps = function th_fps(update, maxFPS, view, renderer) {
    var stats = new Stats()
    stats.showPanel( 0 ); // 0: fps, 1: ms, 2: mb, 3+: custom
    document.body.appendChild( stats.dom );

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

