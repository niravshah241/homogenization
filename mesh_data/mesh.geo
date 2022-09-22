wsub1 = 0.2;
wsub2 = 0.1;
hsubs = 0.5;

//Subdomain 1
h1 = 0.1;
Point(1) = {0,0,0,h1};
Point(2) = {0,hsubs,0,h1};
Point(3) = {wsub1,hsubs,0,h1};
Point(4) = {wsub1,0,0,h1};

//Subdomain 1
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};
Line Loop(1) = {1,2,3,4};
Physical Line(1) = {1};//Left boundary
Physical Line(2) = {2};//Top boundary
Physical Line(3) = {4};//Bottom boundary

//Subdomain 1
Plane Surface(1) = {1};
Physical Surface(1) = {1};

//Subdomain 2
h2 = 0.05;
//Point(4) = {wsub1,0,0,h2};
//Point(3) = {wsub1,hsubs,0,h2};
Point(5) = {wsub1+wsub2,hsubs,0,h2};
Point(6) = {wsub1+wsub2,0,0,h2};

//Subdomain 2
//Line(-3)
Line(5) = {3,5};
Line(6) = {5,6};
Line(7) = {6,4};
Line Loop(2) = {-3,5,6,7};
Physical Line(4) = {5};//Top boundary
Physical Line(5) = {6};//Right boundary
Physical Line(6) = {7};//Bottom boundary

//Subdomain 2
Plane Surface(2) = {2};
Physical Surface(2) = {2};
