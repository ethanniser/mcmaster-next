import { eq, isNotNull, isNull } from "drizzle-orm";
import { db } from "../src/db";
import { categories, products, subcategories } from "../src/db/schema";
import { Effect, Array, Predicate, Random } from "effect";
import { NodeRuntime } from "@effect/platform-node";

const main = Effect.gen(function* () {
  const categoryUrls = yield* Effect.tryPromise(() =>
    db
      .select({ imageUrl: categories.image_url })
      .from(categories)
      .where(isNotNull(categories.image_url)),
  );

  const subcategoryUrls = yield* Effect.tryPromise(() =>
    db
      .select({ imageUrl: subcategories.image_url })
      .from(subcategories)
      .where(isNotNull(subcategories.image_url)),
  );

  const productUrls = yield* Effect.tryPromise(() =>
    db
      .select({ imageUrl: products.image_url })
      .from(products)
      .where(isNotNull(products.image_url)),
  );

  const allUrls = Array.dedupe(
    Array.filter(
      [
        ...categoryUrls.map((c) => c.imageUrl),
        ...subcategoryUrls.map((s) => s.imageUrl),
        ...productUrls.map((p) => p.imageUrl),
      ],
      Predicate.isNotNull,
    ),
  );

  yield* Effect.log(`Total unqiue image urls found: ${allUrls.length}`);

  const productsWithoutImage = yield* Effect.tryPromise(() =>
    db
      .select({ slug: products.slug })
      .from(products)
      .where(isNull(products.image_url)),
  );

  yield* Effect.log(
    `Products without image urls found: ${productsWithoutImage.length}`,
  );

  yield* Effect.all(
    productsWithoutImage.map((product, i) =>
      Effect.gen(function* () {
        yield* Effect.log(
          `Beginning update for index ${i} of ${productsWithoutImage.length}`,
        );
        const randomImageUrl = yield* Random.choice(allUrls);
        yield* Effect.tryPromise(() =>
          db
            .update(products)
            .set({ image_url: randomImageUrl })
            .where(eq(products.slug, product.slug)),
        );
      }),
    ),
    { mode: "either", concurrency: 10 },
  );
});

NodeRuntime.runMain(main);
