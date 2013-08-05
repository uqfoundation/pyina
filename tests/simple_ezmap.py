# 

if __name__ == '__main__':
    # get the parallel mapper
    from pyina.ez_map import ez_map

    # construct a target function
    def host(id):
        import socket
        return "Rank: %d -- %s" % (id, socket.gethostname())

    # launch the parallel map of the target function
    results = ez_map(host, range(10), nodes=4)
    print "\n".join(results)

    # print launch command for all launchers
    from pyina.launchers import all_launches
    print "\n", all_launches()


# EOF
