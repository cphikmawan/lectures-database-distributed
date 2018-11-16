rsconf = {
    _id : "rs0",
    members: [
        { _id : 0, host : "db-manager:27017" },
        { _id : 1, host : "db-node1:27017" },
        { _id : 2, host : "db-node2:27017" }
    ]
}

rs.initiate(rsconf);

rs.conf();