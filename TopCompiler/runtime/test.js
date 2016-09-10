//<List>

//reverse
assertEq(newList(0,1,2).reverse(), newList(2,1,0));

//append
assertEq(EmptyList.append(10), newList(10));

//insertAt
assertEq(newList(10, 20, 30).insert(-1, 20), newList(10, 20, 20, 30));

//copy

var b = newList(10,20);
var t = b.copy()

assertEq(t, newList(10,20));

//concat
assertEq(newList(10,20).operator_add(newList(30,40)), newList(10,20,30,40));

//delete
assertEq(newList(10,20,30).del(1), newList(10,30));

//set
assertEq(newList(20,20).set(1, 10).set(0, 10), newList(10, 10));

//<Vector>
//insert
assertEq(newVector(1,2,3).insert(0, 0), newVector(0,1,2,3))

//set
assertEq(newVector(1,1,2,3).set(0,0), newVector(0,1,2,3))

//add
assertEq(newVector(1,2,3).operator_add(newVector(4,5,6)), newVector(1,2,3,4,5,6))