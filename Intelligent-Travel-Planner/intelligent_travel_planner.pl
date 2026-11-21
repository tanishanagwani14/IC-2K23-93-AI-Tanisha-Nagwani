
% ==========================================
% INTELLIGENT TRAVEL PLANNER
% MCA - ARTIFICIAL INTELLIGENCE LAB TEST 2
% Developed as a custom route recommendation system
% ==========================================

% connection(Source, Destination, Cost, Time, Distance)

link(delhi, jaipur, 2500, 5, 280).
link(delhi, agra, 1800, 4, 230).
link(delhi, lucknow, 3200, 8, 550).
link(agra, jaipur, 1500, 4, 240).
link(agra, lucknow, 2100, 5, 335).
link(jaipur, bhopal, 3500, 8, 600).
link(jaipur, mumbai, 9000, 17, 1150).
link(lucknow, bhopal, 2800, 7, 570).
link(lucknow, mumbai, 7500, 18, 1350).
link(bhopal, mumbai, 4000, 10, 780).
link(bhopal, pune, 3000, 7, 600).
link(mumbai, pune, 1200, 3, 150).

% Connections work in both directions

connection(A, B, C, T, D) :-
    link(A, B, C, T, D),
    \+ unavailable(A, B),
    \+ unavailable(B, A).

connection(A, B, C, T, D) :-
    link(B, A, C, T, D),
    \+ unavailable(A, B),
    \+ unavailable(B, A).

% Temporarily closed road
unavailable(delhi, agra).

% Find routes without visiting the same city twice

travel_path(Source, Destination, Avoid, Path) :-
    Source \= Avoid,
    Destination \= Avoid,
    search_path(Source, Destination, [Source], Avoid, Rev),
    reverse(Rev, Path).

search_path(Destination, Destination, Visited, _, Visited).

search_path(Current, Destination, Visited, Avoid, Path) :-
    connection(Current, Next, _, _, _),
    Next \= Avoid,
    \+ member(Next, Visited),
    search_path(Next, Destination, [Next|Visited], Avoid, Path).

% Calculate total cost, time and distance

calculate_totals([_], 0, 0, 0).

calculate_totals([A,B|Rest], Cost, Time, Distance) :-
    connection(A, B, C1, T1, D1),
    calculate_totals([B|Rest], C2, T2, D2),
    Cost is C1 + C2,
    Time is T1 + T2,
    Distance is D1 + D2.

% Choose the value according to preference

% Route preference values
preference_value(cheapest, C, _, _, C).
preference_value(fastest, _, T, _, T).
preference_value(shortest, _, _, D, D).

% Find the best available route
best_route(Source, Destination, Preference, Avoid,
           Path, Cost, Time, Distance) :-

    findall(Key-result(P,C,T,D),
        (
            travel_path(Source, Destination, Avoid, P),
            calculate_totals(P, C, T, D),
            preference_value(Preference, C, T, D, Key)
        ),
        Routes),

    keysort(Routes, [_-result(Path,Cost,Time,Distance)|_]).

% Display route
display_path([City]) :-
    write(City).

display_path([City|Rest]) :-
    write(City),
    write(' -> '),
    display_path(Rest).

% Display recommendation
planner(Source, Destination, Preference, Avoid) :-
    nl,
    write('================================'), nl,
    write('     INTELLIGENT TRAVEL PLANNER'), nl,
    write('================================'), nl,

    write('Source: '), write(Source), nl,
    write('Destination: '), write(Destination), nl,
    write('Preference: '), write(Preference), nl,

    (
        best_route(Source, Destination, Preference, Avoid,
                   Path, Cost, Time, Distance)
        ->
        write('Recommended Route: '),
        display_path(Path), nl,

        write('Total Cost: Rs. '), write(Cost), nl,
        write('Travel Time: '), write(Time), write(' hours'), nl,
        write('Total Distance: '), write(Distance),
        write(' km'), nl,

        write('Reason: Selected according to '),
        write(Preference), write(' preference.'), nl
        ;
        write('No available route found.'), nl
    ).

% Display all possible routes
show_routes(Source, Destination) :-
    findall(P-C-T-D,
        (
            travel_path(Source, Destination, none, P),
            calculate_totals(P, C, T, D)
        ),
        Routes),
    nl,
    write('AVAILABLE ROUTES:'), nl,
    print_routes(Routes).

print_routes([]).

print_routes([P-C-T-D|Rest]) :-
    display_path(P), nl,
    write('Cost: Rs. '), write(C),
    write(' | Time: '), write(T),
    write(' hours | Distance: '), write(D),
    write(' km'), nl,
    print_routes(Rest).

% Compare cheapest and fastest
compare_routes(Source, Destination) :-
    nl,
    write('CHEAPEST ROUTE:'), nl,
    planner(Source, Destination, cheapest, none),
    nl,
    write('FASTEST ROUTE:'), nl,
    planner(Source, Destination, fastest, none).

% Interactive Travel Planner

% Input Validation

valid_city(delhi).
valid_city(jaipur).
valid_city(agra).
valid_city(lucknow).
valid_city(bhopal).
valid_city(mumbai).
valid_city(pune).

valid_preference(cheapest).
valid_preference(fastest).
valid_preference(shortest).

% Interactive Travel Planner

start :-
    nl,
    write('===== INTELLIGENT TRAVEL PLANNER ====='), nl,

    write('Available Cities: delhi, jaipur, agra, lucknow, bhopal, mumbai, pune'), nl,

    write('Enter Source City: '),
    read(Source),

    write('Enter Destination City: '),
    read(Destination),

    write('Choose Preference (cheapest/fastest/shortest): '),
    read(Preference),

    (
        valid_city(Source),
        valid_city(Destination),
        valid_preference(Preference)
        ->
        planner(Source, Destination, Preference, none)
        ;
        write('Invalid Input! Please enter valid cities and preference.'), nl
    ).
