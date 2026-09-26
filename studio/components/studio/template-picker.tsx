/* eslint-disable @next/next/no-img-element */
"use client"

import type { KeyboardEvent, ReactNode } from "react"
import {
  Bird,
  Clapperboard,
  Flame,
  Gem,
  MoonStar,
  Sparkles,
  type LucideIcon,
} from "lucide-react"

import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

/**
 * Templates — the "what you can make" examples. A `TemplateItem` seeds the
 * prompt dock (prompt text + optional model/settings) when its Try action fires.
 * `TemplateCard` and `ExamplePresets` render them; the Explore tab on Home uses
 * `ExamplePresets`.
 */

// The Raven Moon artwork — original gothic illustrations in /presets/*.svg.
const ART = {
  ravenMoon: "/presets/raven-moon.svg",
  blackRose: "/presets/black-rose.svg",
  roseWindow: "/presets/rose-window.svg",
  moonPhases: "/presets/moon-phases.svg",
  tarotCard: "/presets/tarot-card.svg",
  ravenFlight: "/presets/raven-flight.svg",
} as const

export interface TemplateItem {
  id: string
  title: string
  subtitle: string
  /** Free-form filter category used by the picker tabs. */
  category: string
  kind: "image" | "video"
  images: [string, string, string]
  icon: LucideIcon
  /** What the Try action puts in the dock. */
  prompt: string
  /** Catalog model id to switch to, when the template needs a specific one. */
  modelId?: string
  settings?: Record<string, unknown>
}

// The Raven Moon presets: artwork for prints and merch, product visuals and
// short motion loops for the shop and social.
export const TEMPLATES: TemplateItem[] = [
  {
    id: "moonlit-raven-print",
    title: "Moonlit raven art print",
    subtitle: "Poster-ready gothic illustration",
    category: "artwork",
    kind: "image",
    images: [ART.ravenMoon, ART.moonPhases, ART.roseWindow],
    icon: MoonStar,
    prompt:
      "Elegant gothic illustration of a black raven perched on a bare branch before a huge ivory full moon, deep plum night sky, fine etched linework, antique gold accents, poster composition with space for a title.",
    modelId: "recraft-4.1",
  },
  {
    id: "tarot-card",
    title: "Tarot card design",
    subtitle: "Gilded card art with a title",
    category: "artwork",
    kind: "image",
    images: [ART.tarotCard, ART.moonPhases, ART.ravenMoon],
    icon: Sparkles,
    prompt:
      'Ornate tarot card design titled "THE RAVEN MOON", crescent moon above an all-seeing eye, gilded art nouveau border, black velvet background, antique gold foil linework, symmetrical and centered.',
    modelId: "ideogram-4",
  },
  {
    id: "velvet-product-still",
    title: "Jewelry on black velvet",
    subtitle: "Candlelit product still",
    category: "product",
    kind: "image",
    images: [ART.blackRose, ART.tarotCard, ART.roseWindow],
    icon: Gem,
    prompt:
      "Luxury product photo of a silver crescent-moon pendant resting on crushed black velvet beside a dark red rose, two dripping candles glowing behind, shallow depth of field, moody chiaroscuro lighting.",
    modelId: "soul-cinema",
  },
  {
    id: "cathedral-moonlight",
    title: "Cathedral moonlight",
    subtitle: "Stained-glass mood still",
    category: "artwork",
    kind: "image",
    images: [ART.roseWindow, ART.ravenMoon, ART.blackRose],
    icon: Bird,
    prompt:
      "Inside an abandoned gothic cathedral at night, moonlight pouring through a violet stained-glass rose window, dust drifting in the beams, a single raven on a stone pew, cinematic and serene.",
    modelId: "soul-cinema",
  },
  {
    id: "candlelit-reveal",
    title: "Candlelit product reveal",
    subtitle: "Slow push-in for the shop",
    category: "product",
    kind: "video",
    images: [ART.blackRose, ART.tarotCard, ART.ravenMoon],
    icon: Flame,
    prompt:
      "Slow cinematic push-in on a gothic silver moon necklace lying on black velvet, candle flames flickering in the background, a dark rose petal falling into frame, warm rim light, elegant and hushed.",
    modelId: "seedance-2.5",
  },
  {
    id: "raven-takes-flight",
    title: "Raven takes flight",
    subtitle: "Looping social clip",
    category: "motion",
    kind: "video",
    images: [ART.ravenFlight, ART.ravenMoon, ART.moonPhases],
    icon: Clapperboard,
    prompt:
      "A black raven spreads its wings and takes flight from a castle spire at dusk, sky fading from ember orange to deep violet, a pale moon rising, graceful slow motion, cinematic wide shot.",
    modelId: "kling-3-std",
  },
]

function gradientFromSeed(seed: string): string {
  let hash = 0
  for (const c of seed) hash = (hash * 31 + c.charCodeAt(0)) >>> 0
  const start = hash % 360
  const end = (start + 36 + ((hash >>> 8) % 72)) % 360
  return `linear-gradient(135deg, hsl(${start} 62% 52%) 0%, hsl(${end} 76% 27%) 100%)`
}

function GradientBadge({ as: Glyph, seed }: { as: LucideIcon; seed: string }) {
  return (
    <span className="relative flex size-9 shrink-0 items-center justify-center overflow-hidden rounded-[10px] border border-white/25 text-white shadow-[0_5px_3px_rgba(0,0,0,0.08),inset_0_3px_5px_rgba(255,255,255,0.24)]">
      <span
        aria-hidden
        className="absolute inset-0"
        style={{ backgroundImage: gradientFromSeed(seed) }}
      />
      <span
        aria-hidden
        className="absolute inset-0 bg-gradient-to-t from-transparent to-white/20 mix-blend-overlay"
      />
      <Glyph className="relative size-5" />
    </span>
  )
}

const TRIPTYCH = [
  "rounded-l-2xl rounded-r-sm",
  "rounded-sm",
  "rounded-r-2xl rounded-l-sm",
] as const

export interface TemplateCardProps {
  template: TemplateItem
  variant?: "single" | "triptych"
  onTry: (template: TemplateItem) => void
  tryLabel?: ReactNode
}

export function TemplateCard({
  template,
  variant = "single",
  onTry,
  tryLabel = "Try",
}: TemplateCardProps) {
  const onKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.currentTarget !== event.target) return
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault()
      onTry(template)
    }
  }
  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={`Use template: ${template.title}`}
      className="relative flex cursor-pointer flex-col gap-2 rounded-[20px] bg-white/5 p-2 shadow-[0_2px_6px_rgba(0,0,0,0.15)] transition-[transform,background-color] duration-200 hover:z-[1] hover:-translate-y-0.5 hover:bg-white/8 focus-visible:ring-2 focus-visible:ring-ring focus-visible:outline-none motion-reduce:hover:translate-y-0"
      onClick={() => onTry(template)}
      onKeyDown={onKeyDown}
    >
      <div className="flex h-60 items-stretch gap-1.5">
        {variant === "triptych" ? (
          template.images.map((src, i) => (
            <div
              key={i}
              className={cn(
                "min-w-0 flex-1 overflow-hidden border border-white/10",
                TRIPTYCH[i]
              )}
            >
              <img
                src={src}
                alt={`${template.title} — shot ${i + 1}`}
                className="size-full object-cover"
              />
            </div>
          ))
        ) : (
          <div className="min-w-0 flex-1 overflow-hidden rounded-2xl border border-white/10">
            <img
              src={template.images[0]}
              alt={template.title}
              className="size-full object-cover"
            />
          </div>
        )}
      </div>
      <div className="flex items-center gap-3 px-2 py-1">
        <GradientBadge as={template.icon} seed={template.id} />
        <div className="flex min-w-0 flex-1 flex-col gap-0.5">
          <span className="truncate text-sm font-medium text-foreground">
            {template.title}
          </span>
          <span className="truncate text-xs text-muted-foreground">
            {template.subtitle}
          </span>
        </div>
        <Button
          size="sm"
          className="rounded-full font-semibold"
          onClick={(event) => {
            event.stopPropagation()
            onTry(template)
          }}
        >
          {tryLabel}
        </Button>
      </div>
    </div>
  )
}

export interface ExamplePresetsProps {
  items: TemplateItem[]
  onUse: (template: TemplateItem) => void
  tryLabel?: ReactNode
  className?: string
}

/** The Explore grid: two columns of `TemplateCard`s. */
export function ExamplePresets({
  items,
  onUse,
  tryLabel = "Try",
  className = "w-full max-w-[900px]",
}: ExamplePresetsProps) {
  return (
    <div
      className={cn("grid w-full grid-cols-1 gap-5 sm:grid-cols-2", className)}
    >
      {items.map((t) => (
        <TemplateCard
          key={t.id}
          template={t}
          onTry={onUse}
          tryLabel={tryLabel}
        />
      ))}
    </div>
  )
}
