//+
Point(1) = {0, 0, 0, 0.01};
//+
Point(2) = {0, 0.5, 0, 0.01};
//+
Point(3) = {0.2, 0.5, 0, 0.01};
//+
Point(4) = {0.2, 0, 0, 0.01};
//+
Point(5) = {0.3, 0.5, 0, 0.01};
//+
Point(6) = {0.3, 0, 0, 0.01};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 1};
//+
Line(5) = {3, 5};
//+
Line(6) = {5, 6};
//+
Line(7) = {6, 4};
//+
Curve Loop(1) = {1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {6, 7, -3, 5};
//+
Plane Surface(2) = {2};
//+
Physical Surface(1) = {1};
//+
Physical Surface(2) = {2};
//+
Physical Line(1) = {1};
//+
Physical Line(2) = {2};
//+
Physical Line(4) = {4};
//+
Physical Line(5) = {5};
//+
Physical Line(6) = {6};
//+
Physical Line(7) = {7};

Mesh.Algorithm = 8;
Mesh.RecombinationAlgorithm = 2;
Mesh.RecombineAll = 1;
Mesh.SubdivisionAlgorithm = 1;
