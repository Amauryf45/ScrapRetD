const username1 = "asso.ema";

// Définissez getResult comme une fonction async pour utiliser await à l'intérieur et retourner une promesse.
async function getResult(username) {
  let followers = [];
  let followings = [];

  try {
    console.log(`Process started for ${username}! Give it a couple of seconds`);

    const userQueryRes = await fetch(
      `https://www.instagram.com/web/search/topsearch/?query=${username}`
    );
    const userQueryJson = await userQueryRes.json();
    const userId = userQueryJson.users.map(u => u.user)
      .filter(u => u.username === username)[0].pk;

    let after = null;
    let has_next = true;

    // Obtenez les followers
    while (has_next) {
      const res = await fetch(
        `https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=` +
        encodeURIComponent(
          JSON.stringify({
            id: userId,
            include_reel: true,
            fetch_mutual: true,
            first: 50,
            after: after,
          })
        )
      ).then(res => res.json());

      has_next = res.data.user.edge_followed_by.page_info.has_next_page;
      after = res.data.user.edge_followed_by.page_info.end_cursor;
      followers = followers.concat(
        res.data.user.edge_followed_by.edges.map(({ node }) => ({
          username: node.username,
          full_name: node.full_name,
        }))
      );
    }

    // Réinitialisez pour obtenir les followings
    after = null;
    has_next = true;

    while (has_next) {
      const res = await fetch(
        `https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=` +
        encodeURIComponent(
          JSON.stringify({
            id: userId,
            include_reel: true,
            fetch_mutual: true,
            first: 50,
            after: after,
          })
        )
      ).then(res => res.json());

      has_next = res.data.user.edge_follow.page_info.has_next_page;
      after = res.data.user.edge_follow.page_info.end_cursor;
      followings = followings.concat(
        res.data.user.edge_follow.edges.map(({ node }) => ({
          username: node.username,
          full_name: node.full_name,
        }))
      );
    }

    // Combine data into a single object
    const resultData = {
      followers: followers,
      followings: followings,
    };

    // Créez un objet Blob
    const blob = new Blob([JSON.stringify(resultData, null, 2)], { type: 'application/json' });

    // Créez un élément de lien
    const link = document.createElement('a');
    link.href = window.URL.createObjectURL(blob);
    link.download = `instagram_results_${username}.json`;
    link.style.display = 'none'; // Rendre le lien non visible
    document.body.appendChild(link); // Ajoutez le lien à la page
    link.click(); // Simuler un clic sur le lien pour télécharger le fichier
    document.body.removeChild(link); // Nettoyez en supprimant le lien de la page

    console.log(`Results processed and saved for ${username}.`);
    return resultData;

  } catch (err) {
    console.log({ err });
    return { err }; // Retourne une erreur pour la gestion ultérieure
  }
}

// Utilisez une fonction async pour attendre le résultat avant de continuer.
async function processResults(username) {
  try {
    let firstRes = await getResult(username);
    for (const following of firstRes.followings) {
      // Attendez le résultat de chaque appel suivant si nécessaire.
      // Sinon, vous pouvez simplement appeler getResult sans await si vous ne traitez pas immédiatement les résultats.
      await getResult(following.username);
    }
  } catch (error) {
    console.error(error);
  }
}

// Exécutez la fonction avec le nom d'utilisateur de départ.
processResults(username1);
