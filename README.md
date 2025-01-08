# git-remote-ipfs

git-remote-ipfs is a transparent bidirectional bridge between Git and
[IPFS](https://ipfs.tech/). It lets you use an IPFS file as a Git remote!

---

This Git remote helper makes IPFS act like a _true Git remote_. It maintains
_all guarantees_ that are provided by a traditional Git remote while using
IPFS as a backing store. This means that it works correctly even when there
are multiple people operating on the repository at once, making it possible to
use a IPFS shared folder as a Git remote for collaboration.

Once the helper is installed, using it is as simple as adding a remote like
`ipfs:///path/to/repo`.

To clone repositories in folders or shared folders mounted in your IPFS, you
can run:

```bash
git clone "ipfs:///path/to/repo"
```

To add a remote to an existing local repository, you can run:

```bash
git remote add origin "ipfs:///path/to/repo"
```

The repository directory will be created automatically the first time you push.

After adding the remote, you can treat it just like a regular Git remote. The
IPFS-backed remote supports all operations that regular remotes support, and
it provides identical guarantees in terms of atomicity even when there are
concurrent operations.

## Design

To read about the design of git-remote-ipfs, see [DESIGN.md](DESIGN.md).
This could be especially useful if you're thinking about contributing to the
project.

## Contributing

Do you have ideas on how to improve git-remote-ipfs? Have a feature request,
bug report, or patch? Great! See [CONTRIBUTING.md](CONTRIBUTING.md) for
information on what you can do about that.

## License

Copyright (c) 2022-2025 Naveen Thota (naveensaisreenivas@gmail.com), Nippun Sharma (inbox.nippun@gmail.com).
Released under the MIT License. See [LICENSE.md](LICENSE.md) for details.

## Inspiration

This work was inspired by [git-remote-dropbox](https://github.com/anishathalye/git-remote-dropbox).
